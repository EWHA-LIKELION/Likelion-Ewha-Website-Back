import sys
import secrets
import string
from typing import List, Tuple, Optional

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounts.models import User


def generate_strong_password(length: int = 20) -> str:
    if length < 12:
        raise ValueError("Password length must be >= 12")

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()-_=+"

    chars = [
        secrets.choice(lower),
        secrets.choice(upper),
        secrets.choice(digits),
        secrets.choice(special),
    ]

    all_chars = lower + upper + digits + special
    chars += [secrets.choice(all_chars) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

# 콘솔 입력값 파싱 함수
def _parse_line(line: str, delimiter: str) -> Tuple[Optional[str], str, Optional[str]]:
    """
    Returns: (email, username, error_message)
    - Accepts: "email,username" or "email"
    - Strips spaces.
    """
    raw = line.strip()
    if not raw:
        return None, "", "empty line"

    parts = [p.strip() for p in raw.split(delimiter, 1)]
    email = parts[0] if parts else ""
    username = parts[1] if len(parts) == 2 else ""

    if not email:
        return None, "", "missing email"

    return email, username, None

class Command(BaseCommand):
    help = (
        "콘솔에서 email,username (또는 email) 라인을 여러 줄로 입력받아 "
        "staff 관리자 계정을 생성하고, 이메일별로 생성된 비밀번호를 콘솔에 출력합니다.\n\n"
        "예)\n"
        "  a@company.com,alice\n"
        "  b@company.com,bob\n"
        "  c@company.com\n\n"
        "입력 종료: mac/linux Ctrl+D, windows Ctrl+Z 후 Enter"
    )
        
    def add_arguments(self, parser):
        parser.add_argument(
            "--delimiter",
            default=",",
            type=str,
            help="입력 라인에서 email과 username을 구분하는 구분자 (기본 ,)",
        )
        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="이미 존재하는 이메일은 에러 대신 스킵합니다.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="DB 반영 없이 생성될 항목과 비밀번호만 출력합니다.",
        )

    def handle(self, *args, **options):
        delimiter: str = options["delimiter"]
        password_length: int = 20
        skip_existing: bool = options["skip_existing"]
        dry_run: bool = options["dry_run"]

        self.stdout.write(
            self.style.SUCCESS(
                "콘솔에 email,username (또는 email) 을 여러 줄로 붙여넣고 입력을 종료하세요. "
                "(mac/linux Ctrl+D, windows Ctrl+Z 후 Enter)"
    )
        )
        
        # stdin 전체 읽기
        try:
            input_text = sys.stdin.read()
        except Exception as e:
            raise CommandError(f"표준입력 읽기 실패: {e}")

        lines: List[str] = input_text.splitlines()

        if not lines:
            raise CommandError("입력 라인이 없습니다. email,username 을 붙여넣어 주세요.")

        created = 0
        skipped = 0
        errors = 0

        # 헤더 출력(email, password, status)
        self.stdout.write("email\tpassword\tstatus")

        for idx, line in enumerate(lines, start=1):
            email, username, err = _parse_line(line, delimiter)
            if err:
                if err == "empty line":
                    skipped += 1
                    continue
                self.stderr.write(f"[line {idx}] 파싱 실패: {err} -> {line!r}")
                errors += 1
                continue
            
            assert email is not None

            try:
                exists = User.objects.filter(email=email).exists()
            except Exception as e:
                self.stderr.write(f"[line {idx}] DB 조회 실패({email}): {e}")
                errors += 1
                continue

            if exists:
                if skip_existing:
                    self.stdout.write(f"{email}\t-\tskipped(existing)")
                    skipped += 1
                    continue
                else:
                    self.stderr.write(f"[line {idx}] 이미 존재하는 이메일: {email} (스킵하려면 --skip-existing)")
                    errors += 1
                    continue

            # 비밀번호 생성 
            try:
                password = generate_strong_password(password_length)
            except Exception as e:
                self.stderr.write(f"[line {idx}] 비밀번호 생성 실패({email}): {e}")
                errors += 1
                continue

            if dry_run:
                self.stdout.write(f"{email}\t{password}\tdry-run")
                created += 1
                continue

            try:
                with transaction.atomic():
                    user = User.objects.create_user(email=email, password=password, username=username)
                    user.is_staff = True
                    user.is_superuser = False
                    user.is_active = True
                    user.save(update_fields=["is_staff", "is_superuser", "is_active"])
                self.stdout.write(f"{email}\t{password}\tcreated")
                created += 1
            except TypeError as e:
                self.stderr.write(
                    f"[line {idx}] create_user 인자 불일치 가능({email}): {e}\n"
                    f"-> UserManager.create_user 시그니처 확인 필요"
                )
                errors += 1
            except Exception as e:
                self.stderr.write(f"[line {idx}] 사용자 생성 실패({email}): {e}")
                errors += 1

        mode = "DRY-RUN" if dry_run else "APPLIED"
        self.stdout.write(f"\n[{mode}] created={created}, skipped={skipped}, errors={errors}")

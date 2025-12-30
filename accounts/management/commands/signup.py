import csv
import os
import secrets
import string
from typing import Dict, List, Tuple

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


class Command(BaseCommand):
    help = "CSV(email, username)를 읽어 staff 관리자 계정을 생성하고, 이메일별로 생성된 비밀번호를 콘솔에 출력합니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--input",
            required=True,
            type=str,
            help="입력 CSV 경로 (예: ./csv/manager.csv)",
        )
        parser.add_argument(
            "--delimiter",
            default=",",
            type=str,
            help="CSV 구분자 (기본 ,)",
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
        input_path: str = options["input"]
        delimiter: str = options["delimiter"]
        password_length: int = 20
        skip_existing: bool = options["skip_existing"]
        dry_run: bool = options["dry_run"]

        if not os.path.exists(input_path):
            raise CommandError(f"입력 CSV가 존재하지 않습니다: {input_path}")

        rows, fieldnames = self._read_csv(input_path, delimiter)

        if "email" not in fieldnames:
            raise CommandError("CSV에 'email' 컬럼이 필요합니다. (username은 선택)")

        created = 0
        skipped = 0
        errors = 0

        # 헤더 출력(email, password, status)
        self.stdout.write("email\tpassword\tstatus")

        for line_no, row in enumerate(rows, start=2):
            email = (row.get("email") or "").strip()
            username = (row.get("username") or "").strip() if "username" in row else ""

            if not email:
                self.stderr.write(f"[line {line_no}] email이 비어 있어 스킵합니다.")
                skipped += 1
                continue

            try:
                exists = User.objects.filter(email=email).exists()
            except Exception as e:
                self.stderr.write(f"[line {line_no}] DB 조회 실패({email}): {e}")
                errors += 1
                continue

            if exists:
                if skip_existing:
                    self.stdout.write(f"{email}\t-\tskipped(existing)")
                    skipped += 1
                    continue
                else:
                    self.stderr.write(f"[line {line_no}] 이미 존재하는 이메일: {email} (스킵하려면 --skip-existing)")
                    errors += 1
                    continue

            # 비밀번호 생성 
            try:
                password = generate_strong_password(password_length)
            except Exception as e:
                self.stderr.write(f"[line {line_no}] 비밀번호 생성 실패({email}): {e}")
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
                    f"[line {line_no}] create_user 인자 불일치 가능({email}): {e}\n"
                    f"-> UserManager.create_user 시그니처 확인 필요"
                )
                errors += 1
            except Exception as e:
                self.stderr.write(f"[line {line_no}] 사용자 생성 실패({email}): {e}")
                errors += 1

        mode = "DRY-RUN" if dry_run else "APPLIED"
        self.stdout.write(f"\n[{mode}] created={created}, skipped={skipped}, errors={errors}")

    def _read_csv(self, path: str, delimiter: str) -> Tuple[List[Dict[str, str]], List[str]]:
        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            if reader.fieldnames is None:
                raise CommandError("CSV 헤더를 읽을 수 없습니다.")
            fieldnames = list(reader.fieldnames)
            rows = [dict(r) for r in reader]
        return rows, fieldnames

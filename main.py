import argparse
import sys
from models import (
    add_course,
    enroll,
    pay,
    list_arrears,
    monthly_income,
    validate_month_format,
    CourseType,
)


VALID_COURSE_TYPES = [ct.value for ct in CourseType]


def month_type(month_str):
    try:
        validate_month_format(month_str)
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))
    return month_str


def main():
    parser = argparse.ArgumentParser(
        description="社区老年大学学员报名和学费管理工具"
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="可用命令"
    )

    add_parser = subparsers.add_parser("add-course", help="添加课程")
    add_parser.add_argument("name", help="课程名称")
    add_parser.add_argument(
        "--type",
        required=True,
        choices=VALID_COURSE_TYPES,
        help=f"课程类型: {', '.join(VALID_COURSE_TYPES)}",
    )
    add_parser.add_argument(
        "--fee", required=True, type=int, help="学期学费（整数分）"
    )
    add_parser.add_argument(
        "--capacity", required=True, type=int, help="最大人数"
    )

    enroll_parser = subparsers.add_parser("enroll", help="学员报名")
    enroll_parser.add_argument("course_name", help="课程名称")
    enroll_parser.add_argument("--name", required=True, help="学员姓名")
    enroll_parser.add_argument("--phone", required=True, help="学员手机号")

    pay_parser = subparsers.add_parser("pay", help="缴费")
    pay_parser.add_argument("course_name", help="课程名称")
    pay_parser.add_argument("--phone", required=True, help="学员手机号")
    pay_parser.add_argument(
        "--amount", required=True, type=int, help="缴费金额（整数分）"
    )
    pay_parser.add_argument(
        "--date", required=True, help="缴费日期（格式: YYYY-MM-DD）"
    )

    subparsers.add_parser("arrears", help="显示已报名但未缴费的学员列表")

    income_parser = subparsers.add_parser("monthly-income", help="某月各课程缴费收入")
    income_parser.add_argument(
        "--month", required=True, type=month_type, help="月份（格式: YYYY-MM）"
    )

    args = parser.parse_args()

    try:
        if args.command == "add-course":
            result = add_course(args.name, args.type, args.fee, args.capacity)
            print(result)

        elif args.command == "enroll":
            result = enroll(args.course_name, args.name, args.phone)
            print(result)

        elif args.command == "pay":
            result = pay(
                args.course_name, args.phone, args.amount, args.date
            )
            print(result)

        elif args.command == "arrears":
            result = list_arrears()
            if not result:
                print("没有欠费学员")
            else:
                for course_name, students in result.items():
                    print(f"\n【{course_name}】")
                    for student in students:
                        print(f"  - {student['name']} ({student['phone']})")

        elif args.command == "monthly-income":
            result = monthly_income(args.month)
            total = 0
            print(f"\n{args.month} 各课程缴费收入：")
            for course_name, income in result.items():
                print(f"  {course_name}: {income} 分")
                total += income
            print(f"  -------------------")
            print(f"  总计: {total} 分")

    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

from storage import load_data, save_data


VALID_COURSE_TYPES = ["艺术", "音乐", "舞蹈", "健身", "手工", "其他"]


def validate_course_type(course_type):
    if course_type not in VALID_COURSE_TYPES:
        raise ValueError(
            f"课程类型必须是以下之一: {', '.join(VALID_COURSE_TYPES)}"
        )


def add_course(name, course_type, fee, capacity):
    validate_course_type(course_type)
    fee = int(fee)
    capacity = int(capacity)
    if fee <= 0:
        raise ValueError("学费必须是正整数")
    if capacity <= 0:
        raise ValueError("最大人数必须是正整数")

    data = load_data()
    if name in data["courses"]:
        raise ValueError(f"课程 '{name}' 已存在")

    data["courses"][name] = {
        "type": course_type,
        "fee": fee,
        "capacity": capacity,
    }
    data["enrollments"][name] = []
    data["payments"][name] = {}
    save_data(data)
    return f"成功添加课程: {name} ({course_type}), 学费: {fee}分, 最大人数: {capacity}"


def enroll(course_name, student_name, phone):
    data = load_data()
    if course_name not in data["courses"]:
        raise ValueError(f"课程 '{course_name}' 不存在")

    course = data["courses"][course_name]
    enrollments = data["enrollments"][course_name]

    for enrollment in enrollments:
        if enrollment["phone"] == phone:
            raise ValueError(
                f"{student_name} ({phone}) 已经报名了课程 '{course_name}'"
            )

    if len(enrollments) >= course["capacity"]:
        raise ValueError(
            f"课程 '{course_name}' 已达到最大人数 {course['capacity']}，无法报名"
        )

    enrollments.append({
        "name": student_name,
        "phone": phone,
    })
    save_data(data)
    return f"{student_name} ({phone}) 成功报名课程 '{course_name}'"


def pay(course_name, phone, amount, date):
    amount = int(amount)
    if amount <= 0:
        raise ValueError("缴费金额必须是正整数")

    data = load_data()
    if course_name not in data["courses"]:
        raise ValueError(f"课程 '{course_name}' 不存在")

    enrollments = data["enrollments"][course_name]
    is_enrolled = any(e["phone"] == phone for e in enrollments)
    if not is_enrolled:
        raise ValueError(
            f"手机号 {phone} 未报名课程 '{course_name}'，无法缴费"
        )

    payments = data["payments"][course_name]
    if phone in payments:
        raise ValueError(
            f"手机号 {phone} 已经为课程 '{course_name}' 缴过费了"
        )

    student_name = next(
        e["name"] for e in enrollments if e["phone"] == phone
    )
    payments[phone] = {
        "name": student_name,
        "amount": amount,
        "date": date,
    }
    save_data(data)
    return f"{student_name} ({phone}) 成功为课程 '{course_name}' 缴费 {amount} 分，日期: {date}"


def list_arrears():
    data = load_data()
    result = {}

    for course_name in data["courses"]:
        enrollments = data["enrollments"][course_name]
        payments = data["payments"][course_name]
        arrears_list = []

        for enrollment in enrollments:
            phone = enrollment["phone"]
            if phone not in payments:
                arrears_list.append({
                    "name": enrollment["name"],
                    "phone": phone,
                })

        if arrears_list:
            result[course_name] = arrears_list

    return result


def monthly_income(month):
    data = load_data()
    result = {}

    for course_name in data["courses"]:
        payments = data["payments"][course_name]
        total = 0

        for payment in payments.values():
            if payment["date"].startswith(month):
                total += payment["amount"]

        result[course_name] = total

    return result

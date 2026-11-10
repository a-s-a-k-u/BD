from importlib import import_module

# Импортируем функции создания таблиц и генерации сущностей из каждого файла
create_tables = import_module("create_tables").create_tables
generate_organization = import_module("generate_E2").generate_organization
generate_user = import_module("generate_E1").generate_user
generate_department = import_module("generate_E3").generate_department
generate_service = import_module("generate_E4").generate_service
generate_regulation = import_module("generate_E5").generate_regulation
generate_regulation_requirement = import_module("generate_E6").generate_regulation_requirement
generate_application = import_module("generate_E7").generate_application
generate_application_document = import_module("generate_E8").generate_application_document
generate_document_version = import_module("generate_E9").generate_document_version
generate_status_event = import_module("generate_E10").generate_status_event
generate_interdept_request = import_module("generate_E11").generate_interdept_request
generate_interdept_response = import_module("generate_E12").generate_interdept_response
generate_accrual = import_module("generate_E13").generate_accrual
generate_payment = import_module("generate_E14").generate_payment
generate_accrual_payment = import_module("generate_E13_").generate_accrual_payment
generate_appointment = import_module("generate_E15").generate_appointment
generate_complaint = import_module("generate_E16").generate_complaint
generate_complaint_decision = import_module("generate_E17").generate_complaint_decision
generate_audit_log = import_module("generate_E18").generate_audit_log


def run_all():


    create_tables()


    generate_organization()            # E2: Организация_заявителя
    generate_user()                    # E1: Пользователь
    generate_department()              # E3: Ведомство
    generate_service()                 # E4: Услуга
    generate_regulation()              # E5: Регламент
    generate_regulation_requirement()  # E6: Требование_регламента
    generate_application()             # E7: Заявление
    generate_application_document()    # E8: Документ_заявления
    generate_document_version()        # E9: Версия_документа
    generate_status_event()            # E10: Событие_статуса
    generate_interdept_request()       # E11: Межвед_запрос
    generate_interdept_response()      # E12: Ответ_на_запрос
    generate_accrual()                 # E13: Начисление
    generate_payment()                 # E14: Платеж
    generate_accrual_payment()         # E13__: Оплата_начисления
    generate_appointment()             # E15: Запись_на_приём
    generate_complaint()               # E16: Жалоба
    generate_complaint_decision()      # E17: Решение_по_жалобе
    generate_audit_log()               # E18: Журнал_аудита


if __name__ == "__main__":
    run_all()
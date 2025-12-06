from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "task_attempts" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "task_number" INT NOT NULL,
    "user_answer" TEXT,
    "status" VARCHAR(16) NOT NULL,
    "is_correct" BOOL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_task_attemp_user_id_d029ab" UNIQUE ("user_id", "task_number")
);
COMMENT ON COLUMN "task_attempts"."task_number" IS 'Номер задачи из файла';
COMMENT ON COLUMN "task_attempts"."user_answer" IS 'Ответ пользователя (если был)';
COMMENT ON COLUMN "task_attempts"."status" IS 'Статус: correct/incorrect/skipped';
COMMENT ON COLUMN "task_attempts"."is_correct" IS 'Верно ли (None для skip)';
COMMENT ON COLUMN "task_attempts"."created_at" IS 'Когда отвечено';
COMMENT ON COLUMN "task_attempts"."user_id" IS 'Пользователь';
COMMENT ON TABLE "task_attempts" IS 'История решений задач';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "task_attempts";"""


MODELS_STATE = (
    "eJztWl9z2jgQ/yoMT+lMrmeMCaRvkJCWawI3CbnrNJdhhC2IB1umtmjCdPLdT/+MV7YhJg"
    "FC074wQtqVV/vbXe2u/aPsBw72ovd9FE2alGJ/SssfSj/KBPmYDfKWD0tlNJ0mi3yCoqEn"
    "6CkjHCBJKVbQMKIhsvmuI+RFmE05OLJDd0rdgHCW/2aGVWnwX6sifk3+W8VibIixXB2VwF"
    "RNjBvJuOokpNVjQVqti1/JYCVjq84lcwKbieaScSyECXaWrFZVjIdibAPh5DZmYYGU7PJQ"
    "ShQHzDwlr9xJEo0AH5BMMct5TUog0hCMba6EGXG/zfCABmNM73DIVHFzU55FbHSowCQzf8"
    "j+3t6yCZc4+AFHnIr/nU4GIxd7jmYxrsNZxfyAzqdirkPomSDkah8O7MCb+SQhns7pXUAW"
    "1C4RRjbGBIeIYr49DWfccsjM85SlxcYkD5CQSBEBj4NHaOZx++PcGfOLJ4ExqCk7INx0mT"
    "SROOCYP+UPs2LVrUb1yGowEiHJYqb+KI+XnF0yCg10++VHsY4okhRCjYneoLKLKzDF9bQm"
    "Y72tUmU8kegycd2VypS+DA3bBr5hrGHk0o/q0sEAVfUY2LGRduNtIpcgxd1jgEh0n4dUHz"
    "8sgSrFloKKCVwAKmXTm0IKgwABwoQKbC+PNCzsHYBtKwA7hbOM+HJq+K4YnivA6re/9Pkm"
    "fhR98/hE95/m5cmn5uXBRfOL2N6fq5XzXvdjTB6wG0reX92T814rhXdEEZ1FWahP7lCYD3"
    "XC8SyUN+yQJrxWAVLydrMqH0p2EIbYpn+6JB5FE3c6xU5BB/PRw8DDZEzv2N/K0QqAYjgq"
    "R+9SilcrpljSAXCjgZIrC0IrCDyMyJLrRWNMYTFknLt3OehmBswDSppzHHQDoqYszZ84MC"
    "/3k1avd675SauTdoTri1ab4SSexYhcivOjoR1irjyW9GXBOWUr1PVxPjo6ZwodR7G+jwev"
    "cJEhEOeq8L4CyVxO9KxnckBc0I+YQpwe8ebK7FYFus5F+6rfvPhbQ/G02W/zFVOLdPHsQd"
    "rnFpuU/u30P5X439LXXrct4AgiOg7FExO6/tcylwnNaDAgwf0AOSDRimdjLWfvzLVSQ8Cx"
    "F1nNyy9De3fpCs/OR5PcPDNO7nUYzoIQu2PyGc8FGh0mESI2ztG+qgiv1TZvFYXH2B7j2c"
    "TQQ3S/qHugmTIlMdVgGShPmlcnzdN2WUAxRPbkHoXOQMOErwRmkJpZ0GaXfNNPzyCCxkKL"
    "/BRcZghPTiEfw7a8gucHWqdyf3k5ClNBLahm8nv5RBvsbGXx3VzuukqsnML5d4W85QqZOd"
    "c4RH7uPdJyx8uLZJ1xM9fJM7XJCkQpTKlzujFLXetiOTbNarVuGtWjRs2q12sNYwFUdmkV"
    "Yq3ORw6allLkV8tivEb9BHleuU5ewAVlWrckMmu1AjURo1paFIk1XbEjN4zoYF3V6lz70I"
    "SQrR4bxtzducT2YfLQM1DSmPYAJBO24CQWDXiDv1Xw3IjVOL5L1u87LNie13V4Vt68Ik0z"
    "R0DvSsugZJX9oAqEUcvNYLcWwg9fcYAuk+psQHzh6xzVGt6nLgZDbOgF9gTnpRZPQA0Y9w"
    "PsCmyxw6arVDwCoEFAgFNWnRwj2HXttWXIPUTGM1Y9MTCdNYNzinEPArTWq7JKwMHli8wh"
    "QL7oaxO9q2sU6eoay7u6Rjq2vuHGoZXxAiPzqlh1FFfHziMQaxu/m4hT55kWo3P+RBYDg6"
    "72/qwGbmQnY1UYfm5QAUQwSsONtG8VfjFDU8KnUnZkU/e7S+frmlqGeQPWtuG7orBNySsk"
    "zgiN5A5RNtoA1uSkN1Xh7OV3/j5ZT6znTJzKdNyX931T33zAr6VSiadiP/t8iT0kIMzaU/"
    "4XWr9aW/5xm830Jg5d+66c005XK4erGuoooXmqo7681fq73bzzdvN3HEbK5YpWBoDllT/8"
    "KK7F7TdRuGusoURF/nMqsGIUq5NWFUrZSikgFJOcpPevq153SYmUsKQUeU3YAW8c16aHJc"
    "+N6O1+qnWFFvmptVQg85FX+nuu1B3PN2jlvSXf5bvax/8BKaAkJg=="
)

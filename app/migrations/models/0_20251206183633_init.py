from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "telegram_id" BIGINT NOT NULL UNIQUE,
    "username" VARCHAR(255),
    "first_name" VARCHAR(255),
    "last_name" VARCHAR(255),
    "is_admin" BOOL NOT NULL DEFAULT False,
    "is_blocked" BOOL NOT NULL DEFAULT False,
    "language_code" VARCHAR(10),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "last_activity" TIMESTAMPTZ
);
COMMENT ON COLUMN "users"."telegram_id" IS 'Telegram ID пользователя';
COMMENT ON COLUMN "users"."username" IS 'Telegram username';
COMMENT ON COLUMN "users"."first_name" IS 'Имя пользователя';
COMMENT ON COLUMN "users"."last_name" IS 'Фамилия пользователя';
COMMENT ON COLUMN "users"."is_admin" IS 'Является ли администратором';
COMMENT ON COLUMN "users"."is_blocked" IS 'Заблокирован ли пользователь';
COMMENT ON COLUMN "users"."language_code" IS 'Код языка';
COMMENT ON COLUMN "users"."created_at" IS 'Дата регистрации';
COMMENT ON COLUMN "users"."updated_at" IS 'Дата последнего обновления';
COMMENT ON COLUMN "users"."last_activity" IS 'Последняя активность';
COMMENT ON TABLE "users" IS 'Пользователи бота';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztWFtzmzgU/iuMn7Iz2Q43x3Tf7CTbeqexO4nT7qTbYWQkY01AuCDaejr57ysJMAewCc"
    "6ldTt9IeToHPno+84NfeuFESZB8uI6IXHvL+1bj6GQiJeK/FjrodWqlEoBR/NAKaZCQ0nQ"
    "POEx8rgQLlCQECHCJPFiuuI0YlL1v1S3jYV8WkQ95/Jpe+p9AOSmeupqNXvvl/qWo6k/Rm"
    "mQK+nSDRx5wg/K/M0vemBnu76b7WW7Pdote9HqVsrop5S4PPIJXyqsP3wUYsow+UqS4t/V"
    "rbugJMAVKiiWGyi5y9crJRsz/rdSlCeeu14UpCErlVdrvozYRpsyLqU+YSRGnMjteZxKhl"
    "gaBDmTBWmZp6VK5iKwwWSB0kDyLK0bNBdCwEMu8iImQ0R4k6gD+vJX/jQNe2A71ontCBXl"
    "yUYyuMuOV549M1QITGa9O7WOOMo0FIwlbpwExI9R6G4DcET9nRjWDO8Hs4DuGdDszXJntP"
    "HZk0VqPU9a+XlpmpY1MHXrxOnbg0Hf0TdENZfaGBuNX0nShEIk6kRWPQoWS9ZkPVHvDcpO"
    "lyjeThi0qbElDtSBrZyLDVmFSslWWdI60gV96oB1iL66AWE+X8oE6PdbcHw3vDx9Pbw8El"
    "p/VNGc5EtmtlYFdkHjhLv7Qlu1+sHgqnLuqEj2YM39finx/DQF6AEsVYwOgCTTLtHOqLIc"
    "2MF/VfJo4iIcUral30RRQBDb0bSBWY29ubB7SLvpwl/LmGYuAO45yiXuGQe2AWmszGY6GL"
    "Yg/RjQb4Cd9Aa/BMizGPC6sdzWgKbTN3KTMEk+BVlHqrWjyfXF6PzyyFCcCyXKd3Qpwdg8"
    "iLxbsm20uIdqYHgYZBsDQJoB2MyAR4A0SAhISgtvCYLHJ/ZBUR4g5qfIJ4JMvGdxrhkeQI"
    "E2EPwo0kCCK3bsOWC+8VnVpbwaeofqaug7i6tcquLvxUSi4yLeBP9MrHAaku0EVC1r6OPc"
    "9EXx8lwJ2EKG3cgCXQPplqWE1aF2noBa63SkTYCDpyxY5zHWQttsfHF+NRtevK1k1Nlwdi"
    "5XTCVd16RHJzWKN5to78ez15r8V7uZTs4VNVHC/Vj9Yqk3u+lJn1DKI5dFX0SnBF9PhbRA"
    "vPopscIPjJiq5U8UMbDo2rCU90FHxo2oIhooBwZQglUabgQbedfx61cJtNz52siOPE4/U7"
    "7eN9Qaxk8QbU/cKzrHVNZCiolQL3tIHqMOiCZc3zQvZ4/v+YcUPQXOjTolb/sWt+DeSgrm"
    "yLv9gmLsNlYiM9ql21wKzbAuQUwMIDhHU/qZ3+8OSUy9ZW/LzW++ctx294tKnfsuf3ffCv"
    "6+Gf3uN6OfSZxIl/YYYoHJg8bXp2uA3VF8/u99mRp7gJir/5wAGnq3kb5tpm8O9RHjhG2Z"
    "z/65mk52TPOlSQ3IayYO+AFTjx9rAU34x8OEtQVFeepK1yrAO7oY/lvH9fTNdFRvR3KDkc"
    "D4h7aXu/8BI0vQsA=="
)

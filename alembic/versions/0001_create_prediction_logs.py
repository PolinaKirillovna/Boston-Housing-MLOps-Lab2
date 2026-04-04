"""create prediction_logs table

Revision ID: 0001_create_prediction_logs
Revises: None
Create Date: 2026-04-04 18:45:00
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_create_prediction_logs"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "prediction_logs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("request_id", sa.String(length=36), nullable=False, unique=True),
        sa.Column("crim", sa.Float(), nullable=False),
        sa.Column("zn", sa.Float(), nullable=False),
        sa.Column("indus", sa.Float(), nullable=False),
        sa.Column("chas", sa.Integer(), nullable=False),
        sa.Column("nox", sa.Float(), nullable=False),
        sa.Column("rm", sa.Float(), nullable=False),
        sa.Column("age", sa.Float(), nullable=False),
        sa.Column("dis", sa.Float(), nullable=False),
        sa.Column("rad", sa.Integer(), nullable=False),
        sa.Column("tax", sa.Integer(), nullable=False),
        sa.Column("ptratio", sa.Float(), nullable=False),
        sa.Column("black", sa.Float(), nullable=False),
        sa.Column("lstat", sa.Float(), nullable=False),
        sa.Column("predicted_medv", sa.Float(), nullable=False),
        sa.Column("model_version", sa.String(length=50), nullable=False),
        sa.Column("source", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index(
        "ix_prediction_logs_request_id",
        "prediction_logs",
        ["request_id"],
        unique=True,
    )
    op.create_index(
        "ix_prediction_logs_created_at",
        "prediction_logs",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_prediction_logs_created_at", table_name="prediction_logs")
    op.drop_index("ix_prediction_logs_request_id", table_name="prediction_logs")
    op.drop_table("prediction_logs")

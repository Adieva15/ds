from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(64) NOT NULL
);
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
    "eJzdVl1vmzAU/SsoT5nUVSkhH9sbybI105JMLd2mVhVywCFWwKZg2kYV/32+BuJAEpZKk5"
    "buCTj3XHzvOfial0bAXOzH5zcxjhoftZcGRQEWNyX8TGugMFQoABzNfUlMBEMiaB7zCDlc"
    "gAvkx1hALo6diIScMCpQmvg+gMwRREI9BSWUPCTY5szDfCkLubsXMKEufsZx8Riu7AXBvl"
    "uqk7iwtsRtvg4lNiDemPLPkgsLzm2H+UlAFT9c8yWjmwRCOaAepjhCHMMKPEqgAygw77Ro"
    "KitWUbIqt3JcvECJz7c6PlIGh1GQUFQTyx49WOX9B11vt3t6q93td4xer9Nv9QVXlrQb6q"
    "VZw0qQ7FVSlvGX8dSCRpnwKXMPgFTmII6yLKm3EtiJMEhiI74r9CcR4STA+6UuZ1Ykd/PU"
    "8+KmakAhd50DBaAsUF/eX/JA9ODOqL/O7a2R1xpPRteWOfkOnQRx/OBLiUxrBBFdousK2u"
    "y+K/uxeYn2c2xdavCo3c6mI6kgi7kXyRUVz7ptQE0o4cym7MlG7taXWKCFMIKpjJXXHUuH"
    "SxTtt7PgV4wUap2odQF6tn1MPb4Uj12jxrof5tXw0rxqdo2KHdM8ostQmsIYWqy29gkAc+"
    "SsnlDk2jsRprND3N1QoAdVBFHkSW2gQ6g/n8omjoiz3Dev80jtxEaKczIj+z+a1/qF0TP6"
    "7a6xGdMbpG46/3kSP4qDFkp6xZ7dSnmb21bvdI7Yt4J1cOPKWFqafLA1XiFiTn+bAl60Wk"
    "cIKFgHBZSxsoBiRY7pnh+Cr9ez6YGfAZVSEfKGigbvXOLwM80nMb8/TVlrVISuS4d+IV5z"
    "Yv6q6jr8NhtUT3N4weBfHy/pb0QT030="
)

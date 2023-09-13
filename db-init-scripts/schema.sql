-- Esquema "accountapi"
CREATE SCHEMA IF NOT EXISTS accountapi AUTHORIZATION postgres;

-- Tabela "accounts" 
CREATE TABLE IF NOT EXISTS accountapi.accounts (
    accountid varchar(255) NOT NULL,
    activecard bool NULL,
    availablelimit float8 NULL,
    CONSTRAINT accounts_pkey PRIMARY KEY (accountid)
);

-- Tabela "transactions"
CREATE TABLE IF NOT EXISTS accountapi.transactions (
    transaction_id uuid NOT NULL,
    account_id varchar(255) NULL,
    merchant varchar(255) NULL,
    amount float8 NULL,
    state varchar(50) NULL,
    transaction_time int8 NULL,
    CONSTRAINT transactions_pkey PRIMARY KEY (transaction_id)
);
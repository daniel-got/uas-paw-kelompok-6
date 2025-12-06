# Backend Python Pyramid
> Kode utama backend python pyramid tugas besar Pemrograman Aplikasi Web

## Installation

### Setup postgres:
1. Buat database
```sh
CREATE DATABASE uas_pengweb;
```
2. Buat user/role
```sh
CREATE USER alembic_user WITH PASSWORD '12345';
CREATE USER app_prod_user WITH PASSWORD '12345';
```
3. Berikan hak akses koneksi database tadi ke semua user diatas
```sh
GRANT CONNECT ON DATABASE uas_pengweb TO alembic_user;
GRANT CONNECT ON DATABASE uas_pengweb TO app_prod_user;
```
4. Masuk ke database
```sh
\c uas_pengweb
```
5. (Setup user alembic) Berikan akses ke alembic_user, line 2 dan 3 opsional jika db kosong
```sh
GRANT USAGE, CREATE ON SCHEMA public TO alembic_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO alembic_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO alembic_user;
```
6. (Setup user prod) Berikan akses ke alembic_user
```sh
GRANT USAGE ON SCHEMA public TO app_prod_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_prod_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_prod_user;
```
7. Beri akses tabel yang dibuat alembic nanti ke user prod
```sh
ALTER DEFAULT PRIVILEGES FOR ROLE alembic_user IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_prod_user;

ALTER DEFAULT PRIVILEGES FOR ROLE alembic_user IN SCHEMA public
GRANT USAGE, SELECT ON SEQUENCES TO app_prod_user;
```


## Usage example

A few motivating and useful examples of how your product can be used. Spice this up with code blocks and potentially more screenshots.

_For more examples and usage, please refer to the [Wiki][wiki]._

## Development setup

Describe how to install all development dependencies and how to run an automated test-suite of some kind. Potentially do this for multiple platforms.

```sh
make install
npm test
```

## Release History

* 0.2.1
    * CHANGE: Update docs (module code remains unchanged)
* 0.2.0
    * CHANGE: Remove `setDefaultXYZ()`
    * ADD: Add `init()`
* 0.1.1
    * FIX: Crash when calling `baz()` (Thanks @GenerousContributorName!)
* 0.1.0
    * The first proper release
    * CHANGE: Rename `foo()` to `bar()`
* 0.0.1
    * Work in progress

## Meta

Your Name – [@YourTwitter](https://twitter.com/dbader_org) – YourEmail@example.com

Distributed under the XYZ license. See ``LICENSE`` for more information.

[https://github.com/yourname/github-link](https://github.com/dbader/)


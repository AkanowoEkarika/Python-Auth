Intern

Task:

Django

Authentication

System

with

PostgreSQL,

Redis

&

Deployment

Company

Bill

Station

–

We

are

revolutionizing

financial

services

with

innovative

Fintech

solutions.

Our

platform

enables

convenient

and

secure

ways

to

purchase

airtime

and

data,

pay

utility

bills,

and

more.


Task

Overview

As

part

of

your

internship,

you

will

be

building

a

simple

User

Authentication

System

using

Django
,

integrated

with

PostgreSQL

and

Redis
,

and

deploying

it

to

a

hosting

platform

like

Railway

or

Render
.

This

task

will

help

you

understand

how

user

management

works

in

modern

backend

systems

while

introducing

you

to

caching

and

deployment.


Task

Requirements

1.

Project

Setup


○

Create

a

new

Django

project

called

auth_service
.


○

Use

PostgreSQL

as

the

database

(instead

of

SQLite).


○

Set

up

environment

variables

for

database

configuration.


2.

User

Account

Management


○

Create

a

User

model

(you

can

extend

AbstractUser

or

use

Django’s

built-in

model).


○

Implement

user

registration

with

the

following

fields:


■

Full

Name


■

Email

(used

as

username)


■

Password


○

Save

users

in

the

PostgreSQL

database.


3.

Migrations


○

Write

and

apply

Django

migrations

to

create

database

tables.


4.

Authentication

(Login)


○

Implement

login

with

JWT

authentication.


○

Only

registered

users

should

be

able

to

log

in.


5.

Forgot

Password

with

Redis

Cache


○

Implement

a

forgot

password

feature:


■

Generate

a

reset

token

when

a

user

requests

a

password

reset.


■

Store

this

token

in

Redis

with

an

expiry

time

(e.g.,

10

minutes).


■

Allow

the

user

to

reset

their

password

using

the

token.


6.

Deployment


○

Deploy

the

application

to

Railway

or

Render
.


○

Ensure

the

following

environment

variables

are

configurable:


■

DATABASE_URL

(PostgreSQL

connection

string)


■

REDIS_URL

(Redis

connection

string)


■

SECRET_KEY


■

DEBUG

flag


7.

Documentation


○

Add

a

README.md

with:


■

Setup

instructions


■

Environment

variable

details


■

API

endpoint

documentation

(use

Swagger/OpenAPI

if

possible)


■

Deployment

link



## Deliverables

●

A

GitHub

repository

containing

the

source

code.


●

Live

deployment

link

on

Railway

or

Render
.


●

README

with

setup,

usage,

and

API

documentation.



Bonus

Points

●

Add

Docker

support

for

local

development.


●

Write

unit

tests

for

registration,

login,

and

password

reset.


●

Implement

rate

limiting

on

login

and

password

reset

endpoints.


@echo off
cd /d %~dp0
call:getname %1%
echo filename = %var%
protoc.exe -I=. --python_out=./  %var%
protoc --doc_out=. --doc_opt=json,%var%.json ./%var%
echo done

:getname
set var=%~nx1









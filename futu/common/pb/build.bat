@echo off
cd /d %~dp0
call:getname %1%
echo filename = %var%
protoc.exe -I=. --python_out=./  %var%
echo done

:getname
set var=%~nx1









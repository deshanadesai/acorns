@echo off
title Tapenade

IF NOT DEFINED TAPENADE_HOME set TAPENADE_HOME="/mnt/d/Documents/programming/tapenade_3.15"
IF NOT DEFINED JAVA_HOME set JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/"
IF NOT DEFINED JAVA_BIN set JAVA_BIN="%JAVA_HOME%\bin\java.exe"

set HEAP_SIZE=-mx256m
set CLASSPATH="%TAPENADE_HOME%/build/libs/tapenade-3.15.jar"
set BROWSER="C:\Program Files\Internet Explorer\iexplore.exe"

"%JAVA_BIN%" %HEAP_SIZE% -classpath %CLASSPATH% -Djava_home="%JAVA_HOME%" -Dtapenade_home=%TAPENADE_HOME% -Dbrowser=%BROWSER% fr.inria.tapenade.toplevel.Tapenade %*

if %time:~0,2% leq 9 (set hour=0%time:~1,1%) else (set hour=%time:~0,2%)
set dateStr=%date:~0,4%%date:~5,2%%date:~8,2%
set timeStr=%dateStr%_%hour%%time:~3,2%%time:~6,2%

if not exist backup mkdir backup
copy /y cxkw.db .\backup\cxkw%timeStr%.db
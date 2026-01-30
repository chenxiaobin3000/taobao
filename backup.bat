set dateStr=%date:~0,4%%date:~5,2%%date:~8,2%
set timeStr=%dateStr%_%time:~0,2%%time:~3,2%%time:~6,2%

if not exist backup mkdir backup
copy /y cxkw.db .\backup\cxkw%timeStr%.db
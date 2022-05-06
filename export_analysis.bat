set export_dir=%~dp0export
set tag=%1
set data=%~dp0%2
echo %data%

IF not exist %export_dir% (mkdir %export_dir%)
docker run -it --rm -v %data%:/usr/src/app/dart/data/ -v %export_dir%:/usr/src/app/dart/export --rm %tag%
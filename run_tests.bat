@ECHO OFF

SET TEST_DB="test.db"

IF EXIST %TEST_DB% DEL /F %TEST_DB%

venv\Scripts\Activate.bat & python -m pytest test/ & IF EXIST %TEST_DB% DEL /F %TEST_DB%
# createDB.sh
#!/bin/bash

# Create the Oracle database.
/opt/oracle/product/19c/dbhome_1/bin/dbca -silent \
  -createDatabase \
  -templateName General_Purpose.dbc \
  -gdbname ORCLCDB \
  -sid ORCLCDB \
  -responseFile NO_VALUE \
  -characterSet AL32UTF8 \
  -memoryPercentage 40 \
  -totalMemory 4096 \
  -emConfiguration NONE \
  -sysPassword oracle \
  -systemPassword oracle \
  -createAsContainerDatabase true \
  -numberOfPDBs 1 \
  -pdbName ORCLPDB1 \
  -pdbAdminPassword oracle \
  -databaseType MULTIPURPOSE \
  -automaticMemoryManagement false \
  -storageType FS \
  -datafileDestination "/opt/oracle/oradata"

# Start the Oracle database.
/opt/oracle/product/19c/dbhome_1/bin/sqlplus / as sysdba <<EOF
startup;
exit;
EOF

# Set the password for the SYS user.
/opt/oracle/product/19c/dbhome_1/bin/sqlplus / as sysdba <<EOF
ALTER USER SYS IDENTIFIED BY oracle;
exit;
EOF

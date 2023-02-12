# stopDB.sh
#!/bin/bash

# Stop the Oracle database.
/opt/oracle/product/19c/dbhome_1/bin/sqlplus / as sysdba <<EOF
shutdown immediate;
exit;
EOF

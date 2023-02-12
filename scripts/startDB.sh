# startDB.sh
#!/bin/bash

# Start the Oracle database.
/opt/oracle/product/19c/dbhome_1/bin/sqlplus / as sysdba <<EOF
startup;
exit;
EOF

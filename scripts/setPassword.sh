# setPassword.sh
#!/bin/bash

# Set the password for the specified user.
/opt/oracle/product/19c/dbhome_1/bin/sqlplus / as sysdba <<EOF
ALTER USER $1 IDENTIFIED BY $2;
exit;
EOF

#!/bin/bash
LOGFILE=/home/jtillery/jframe/jframe.log

echo "[jframe_update.sh] Starting update of jframe" >>$LOGFILE
/home/jtillery/jframe/jframe.py jtilleryframe@tilleryweb.com "&qlnf=B7YsrNItfa" /JaneFrame /home/jtillery/Pictures/ >>$LOGFILE 2>&1
if [ $? -eq 188 ]; then
    echo "[jframe_update.sh] Pictures downloaded and/or deleted. Clearing cache & restarting picframe" >>$LOGFILE
    systemctl --user stop picframe.service >>$LOGFILE 2>&1
    rm -f /home/jtillery/picframe_data/data/pictureframe.db3 >>$LOGFILE 2>&1
    systemctl start --user picframe.service >>$LOGFILE 2>&1
    sleep 1
    if ! systemctl --user is-active --quiet picframe.service; then
        echo "[jframe_update.sh] picframe.service failed to restart. Rebooting the machine." >>$LOGFILE
        sudo reboot
    fi
fi
fi
/home/jtillery/jframe/log_maint.sh /home/jtillery/jframe/jframe.log >>$LOGFILE 2>&1
echo "[jframe_update.sh] Update of jframe complete" >>$LOGFILE

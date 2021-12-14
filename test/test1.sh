#!/usr/bin/env bash
ip1=192.168.0.1
ip2=173.194.222.113
ip3=87.250.250.242
i=0
while (($i==0))
do
    for j in {$ip1,$ip2,$ip3}
    do
      nmap -sP --host-timeout 1 $j | grep "Host is up" 1>/dev/null
      if [[ "$?" = "1" ]]
      then
        echo "$(date) $j is not alive" >> test1.log
        i=1
      fi
    done
done
exit 0

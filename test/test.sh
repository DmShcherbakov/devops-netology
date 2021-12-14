#!/usr/bin/env bash
ip1=192.168.0.1
ip2=173.194.222.113
ip3=87.250.250.242
for i in {1..5}
  do
    echo ------ $(date) ------ >> test.log
    for j in {$ip1,$ip2,$ip3}
      do
        echo $j
        echo "******** $j ********" >> test.log
        nmap -p 80 $j >> test.log
      done
    echo ===================== >> test.log
  done
exit 0

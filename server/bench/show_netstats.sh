while [ 1 ]
do
	sleep 1s
	echo "\
ESTABLISHED: $(netstat -t -n -v | grep ESTABLISHED | wc -l)   |   \
TIME_WAIT: $(netstat -t -n -v | grep TIME_WAIT | wc -l)   |   \
CLOSE_WAIT : $(netstat -t -n -v | grep TIME_WAIT | wc -l)\
"
done

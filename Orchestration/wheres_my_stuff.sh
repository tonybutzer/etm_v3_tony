for i in `cat junk` ; do echo $i; aws s3 ls ws-out/CONUS/$i ;echo '---------------' ; done


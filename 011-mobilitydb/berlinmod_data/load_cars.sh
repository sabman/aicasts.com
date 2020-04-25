curl -X POST -k \
    -H "Transfer-Encoding: chunked" \
    -H "Content-Type: application/octet-stream" \
    --data-binary @datamcar.csv \
    "https://localhost.lan/user/rasul/api/v2/sql/copyfrom?api_key=b5ea4fd859ec55a4ff965bb1a2b382487130967c&q=COPY+cars(carid,licence,type,model)+FROM+STDIN+WITH+(FORMAT+csv,+HEADER)"

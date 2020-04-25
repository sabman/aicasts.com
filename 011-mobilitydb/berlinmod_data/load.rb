require 'net/http'
require 'uri'
require 'openssl'

cdbhost="https://localhost.lan"
user="rasul"
api_key="b5ea4fd859ec55a4ff965bb1a2b382487130967c"
sqlendpoint="#{cdbhost}/user/#{user}/api/v2/sql"
query="COPY+cars(carid,licence,type,model)+FROM+STDIN+WITH+(FORMAT+csv,+HEADER)"
uri = URI.parse("#{sqlendpoint}/copyfrom?api_key=#{api_key}&q=#{query}")

datafile = "/Users/shoaib/Downloads/geodata/berlinmod_data/datamcar.csv"
request = Net::HTTP::Post.new(uri)
request.content_type = "application/octet-stream"
request["Transfer-Encoding"] = "chunked"
request.body = ""
request.body << File.read(datafile).delete("\r\n")

req_options = {
  use_ssl: uri.scheme == "https",
  verify_mode: OpenSSL::SSL::VERIFY_NONE,
}

response = Net::HTTP.start(uri.hostname, uri.port, req_options) do |http|
  http.request(request)
end

puts response.to_hash

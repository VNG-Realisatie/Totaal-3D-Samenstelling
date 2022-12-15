FROM ubuntu:20.04

RUN apt-get update && apt-get install -y wget unzip

RUN wget https://s3.amazonaws.com/ifcopenshell-builds/IfcConvert-v0.6.0-517b819-linux64.zip
RUN unzip IfcConvert-v0.6.0-517b819-linux64.zip

ENTRYPOINT ["./IfcConvert"]
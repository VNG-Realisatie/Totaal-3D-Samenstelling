# TODO: Remove sources after build (in same layer)
FROM amrit3701/freecad-cli:latest

ENV GIT_SSL_NO_VERIFY=true

RUN apt-get -y update && \
    apt-get install -y libqt4-dev cmake xvfb && \
    apt-get install -y python3-pyside && \
    apt-get install zip unzip

# Install IfcOpenShell
RUN wget https://s3.amazonaws.com/ifcopenshell-builds/ifcopenshell-python-39-v0.6.0-517b819-linux64.zip
RUN unzip ifcopenshell-python-39-v0.6.0-517b819-linux64.zip

COPY obj2ifc.py /
ENTRYPOINT ["python3", "obj2ifc.py"]
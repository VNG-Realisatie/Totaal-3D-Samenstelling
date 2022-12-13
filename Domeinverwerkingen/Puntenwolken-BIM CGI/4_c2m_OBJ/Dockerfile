# TODO: Remove sources after build (in same layer)
FROM ubuntu:20.04

ENV GIT_SSL_NO_VERIFY=true

# Install base requirements
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -yq qtdeclarative5-dev \
    build-essential g++ git cmake libqt5svg5-dev qttools5-dev unzip wget apt-utils \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libeigen3-dev \
    libqt5opengl5-dev \
    libswscale-dev \
    libtbb-dev \
    libxerces-c-dev \
    libssl-dev \
    python3-dev \
    python3-setuptools \
    libpng-dev \
    libusb-dev \
    libpcap-dev \
    python3-vtk7 \
    libpcl-dev \
    xvfb \
    python3-pip

# GDAL
RUN apt-get update && \
    apt-get install -y libproj-dev libgdal-dev && \
    apt-get upgrade -y && \
    apt-get install -y gdal-bin python3-gdal libgeotiff-dev libjsoncpp-dev

# LASZIP
# https://github.com/LASzip/LASzip.git
RUN mkdir -p /tmp/LASzip && \
    cd /tmp/LASzip && \
    git init && \
    git remote add origin https://github.com/LASzip/LASzip.git && \
    git fetch --tags && \
    latestTag=$(git describe --tags `git rev-list --tags --max-count=1`) && \
    cd /root && rm -rf /tmp/LASzip && \
    git clone --branch $latestTag --depth 1 https://github.com/LASzip/LASzip.git LASzip
RUN mkdir -p /root/LASzip/build && \
    cd /root/LASzip/build && \
    cmake -G "Unix Makefiles" -H/root/LASzip -B/root/LASzip/build \
    && make && \
    make install

# EIGEN
RUN wget --no-check-certificate https://launchpad.net/ubuntu/+archive/primary/+sourcefiles/eigen3/3.3.4-2/eigen3_3.3.4.orig.tar.bz2 && \
    tar xvjf eigen* && \
    cd eigen-eigen* && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release \
    .. && \
    make && \
    make install

# PDAL
# https://pdal.io/development/compilation/unix.html
# https://github.com/CloudCompare/CloudCompare/blob/master/BUILD.md#optional-setup-for-las-using-pdal
RUN mkdir -p /tmp/PDAL && \
    cd /tmp/PDAL && \
    git init && \
    git remote add origin https://github.com/PDAL/PDAL.git && \
    git fetch --tags && \
    latestTag=$(git describe --tags `git rev-list --tags --max-count=1`) && \
    cd /root && rm -rf /tmp/PDAL && \
    git clone --branch $latestTag --depth 1 https://github.com/PDAL/PDAL.git PDAL
RUN mkdir -p /root/PDAL/build && \
    cd /root/PDAL/build && \
    cmake -G "Unix Makefiles" -H/root/PDAL -B/root/PDAL/build \
    -DCMAKE_BUILD_TYPE=Release \
    -DWITH_TESTS=OFF \
    -DWITH_LASZIP=ON \
    -DBUILD_PLUGIN_PYTHON=ON \
    -DBUILD_PLUGIN_PGPOINTCLOUD=ON \
    && make && \
    make install

# Install CloudCompare
# use Dflags for enabled plugins
RUN cd /root && git clone --recursive https://github.com/cloudcompare/CloudCompare.git && \
    mkdir -p /root/CloudCompare/build && \
    cd /root/CloudCompare/build && \
    git submodule init && \
    git submodule update && \
    cmake -G "Unix Makefiles" -H/root/CloudCompare -B/root/CloudCompare/build \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/opt/CloudCompare \
    -DPLUGIN_STANDARD_QHOUGH_NORMALS=ON \
    -DEIGEN_ROOT_DIR=/usr/include/eigen3 \
    -DPLUGIN_STANDARD_QPCL=ON \
    -DPLUGIN_IO_QADDITIONAL=ON \
    -DPLUGIN_IO_QCORE=ON \
    -DPLUGIN_IO_QE57=ON \
    -DPLUGIN_IO_QPDAL=TRUE \
    -DPLUGIN_IO_QPHOTOSCAN=ON \
    -DOPTION_USE_GDAL=ON \
    -DCOMPILE_CC_CORE_LIB_WITH_TBB=ON \
    -DCOMPILE_CC_CORE_LIB_WITH_CGAL=ON \
    -DJSON_ROOT_DIR=/usr/include/jsoncpp \
    && \
    make && \
    make install

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN /sbin/ldconfig -v
ENV LD_LIBRARY_PATH="/opt/CloudCompare/lib:$LD_LIBRARY_PATH"
ENV PATH="/opt/CloudCompare/bin:$PATH"

COPY c2m_obj.py /
ENTRYPOINT ["python3", "c2m_obj.py"] 
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y cmake wget build-essential libeigen3-dev
RUN ln -s /usr/include/eigen3/Eigen /usr/include/Eigen
RUN wget --no-check-certificate https://github.com/CGAL/cgal/releases/download/v5.3/CGAL-5.3.tar.xz
RUN tar -xvf CGAL-5.3.tar.xz 
# RUN mv CGAL-5.3/include/CGAL /usr/include
RUN cd CGAL-5.3 && cmake . && make install

# GLPK
RUN apt-get install -y wget cmake g++ m4 xz-utils libgmp-dev unzip zlib1g-dev libboost-program-options-dev libboost-serialization-dev libboost-regex-dev libboost-iostreams-dev libtbb-dev libreadline-dev pkg-config git liblapack-dev libgsl-dev flex bison libcliquer-dev gfortran-7 file dpkg-dev libopenblas-dev  rpm

RUN apt-get install -y glpk-utils libglpk-dev glpk-doc libmpfr-dev

RUN mkdir /usr/myapp && cd /usr/myapp
RUN mkdir /usr/myapp/data
WORKDIR /usr/myapp

COPY CMakeLists_GLPK.txt ./CMakeLists.txt

COPY planereconstruct.cpp ./planereconstruct.cpp
# RELEASE
# COPY Polygonal_surface_reconstruction.h /usr/include/CGAL/Polygonal_surface_reconstruction.h
RUN cmake -DCGAL_DIR=/usr/include/CGAL -DCMAKE_C_COMPILER=/usr/bin/gcc -DCMAKE_CXX_COMPILER=/usr/bin/g++ -DCMAKE_BUILD_TYPE=Release .
# DEBUG:
# RUN cmake -DSCIP_DIR=/SCIPOptSuite-7.0.3-Linux/lib/cmake/scip -DCGAL_DIR=/usr/include/CGAL -DCMAKE_C_COMPILER=/usr/bin/gcc -DCMAKE_CXX_COMPILER=/usr/bin/g++ -DCMAKE_BUILD_TYPE=Debug .
RUN make

ENTRYPOINT [ "/usr/myapp/planereconstruct" ]
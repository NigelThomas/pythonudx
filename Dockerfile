FROM sqlstream/minimal:7.3.4

USER root
RUN apt-get update && apt-get install -y python3-numpy
USER sqlstream

FROM ubuntu:latest
LABEL authors="yaroslavmalinin"

ENTRYPOINT ["top", "-b"]
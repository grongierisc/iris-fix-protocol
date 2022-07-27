FROM python:3.9
ENV WORKING_DIR /app
WORKDIR ${WORKING_DIR}

COPY ./acceptor/requirements.txt ${WORKING_DIR}/requirements.txt
COPY ../quickfix_binary-1.15.1-cp39-cp39-manylinux_2_24_x86_64.manylinux_2_27_x86_64.whl .
RUN pip install -U pip && pip install -r ${WORKING_DIR}/requirements.txt



ADD . ${WORKING_DIR}
RUN rm -fr ${WORKING_DIR}/initiator/Logs/*
RUN rm -fr ${WORKING_DIR}/initiator/Sessions/*
RUN rm -fr ${WORKING_DIR}/acceptor/Logs/*
RUN rm -fr ${WORKING_DIR}/acceptor/Sessions/*

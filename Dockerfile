FROM python:3.10


RUN pip install selenium
RUN pip install webdriver_manager
RUN pip install random-user-agent
COPY . /usr/src/Scrapper/
WORKDIR /usr/src/Scrapper
ENV PYTHONPATH /usr/src

CMD ["python","-u","DistrictPlacesScrapper.py"]
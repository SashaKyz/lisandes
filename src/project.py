import jaydebeapi;
from elasticsearch import Elasticsearch;
import yaml;


class GetItemCount:

    def ReadConfig(self):
        with open(self.filename, "r") as f:
            self.config = yaml.safe_load(f)
        self.LIS_query = "SELECT COUNT(*) FROM " + self.config['lisDataSourceFactory']['properties'][
            'hibernate.default_catalog'] + "." + self.config['lisDataSourceFactory']['properties'][
                             'hibernate.default_schema'] + ".lis_fac_file lisfacfile0_ WHERE lisfacfile0_.fac_type IN  (400, 403, 430, 431, 433, 710, 711, 720, 721, 722, 726, 728, 729, 730, 731, 732, 733);"

    def GetItemCount_LIS(self):
        conn = jaydebeapi.connect(
            self.config['lisDataSourceFactory']['properties']['hibernate.connection.driver_class'],
            self.config['lisDataSourceFactory']['properties']['hibernate.connection.url'],
            [self.config['lisDataSourceFactory']['properties']['hibernate.connection.username'],
             self.config['lisDataSourceFactory']['properties']['hibernate.connection.password']],
            "connxjdbc.jar", )
        curs = conn.cursor()
        curs.execute(self.LIS_query)
        self.lis_numbers = curs.fetchone()[0]
        curs.close()
        conn.close()
        return self.lis_numbers

    def GetItemCount_ES(self):
        es = Elasticsearch(
            self.config['elasticsearch']['elasticsearch.additional.nodes'],
            http_auth=(self.config['elasticsearch']['elasticsearch.xpack.user'],
                       self.config['elasticsearch']['elasticsearch.xpack.password']),
        )
        alias_lst = next(
            iter(es.indices.get_alias(index=self.config['elasticsearch']['elasticsearch.index.prefix'] + '*',
                                      name=self.config['elasticsearch']['elasticsearch.alias']).keys()))
        self.es_numbers = es.count(index=alias_lst)["count"]
        return self.es_numbers

    def ShowItemCount_ES(self):
        print("ElasticSearch shows {} items".format(self.es_numbers))

    def ShowItemCount_LIS(self):
        print("LIS database shows {} items".format(self.lis_numbers))

    def ShowItemCount(self):
        self.ShowItemCount_ES()
        self.ShowItemCount_LIS()

    def ItemCompare_ES_LIS(self):
        print("ElasticSearch shows {} items and LIS database shows {} items".format(self.es_numbers, self.lis_numbers))
        if (self.es_numbers > self.lis_numbers):
            print("ElasticSearch have more records that LIS")
        elif (self.es_numbers < self.lis_numbers):
            print("ElasticSearch have less records that LIS")
        else:
            print("ElasticSearch have the same number of records that LIS")

    def __init__(self, fname="elasticsearch.yml"):
        self.filename = fname
        self.ReadConfig()
        self.lis_number = self.GetItemCount_LIS()
        self.es_number = self.GetItemCount_ES()

Item_count=GetItemCount("/elasticsearch.yml")
Item_count.ItemCompare_ES_LIS()
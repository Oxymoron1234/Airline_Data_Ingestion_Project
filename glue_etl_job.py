import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node DailyFlightsRawFromS3
DailyFlightsRawFromS3_node1738383406049 = glueContext.create_dynamic_frame.from_catalog(database="airlines", table_name="flights_raw", transformation_ctx="DailyFlightsRawFromS3_node1738383406049")

# Script generated for node AirportCodesDim
AirportCodesDim_node1738383311601 = glueContext.create_dynamic_frame.from_catalog(database="airlines", table_name="dev_airlines_dim_airport_codes", redshift_tmp_dir="s3://redshift-data-gds-new/read/",additional_options={"aws_iam_role": "arn:aws:iam::851725469799:role/redshift_role"}, transformation_ctx="AirportCodesDim_node1738383311601")

# Script generated for node JoinForDepartureDetails
JoinForDepartureDetails_node1738383508715 = Join.apply(frame1=DailyFlightsRawFromS3_node1738383406049, frame2=AirportCodesDim_node1738383311601, keys1=["originairportid"], keys2=["airport_id"], transformation_ctx="JoinForDepartureDetails_node1738383508715")

# Script generated for node SchemaChangesForDepartureDetails
SchemaChangesForDepartureDetails_node1738383649894 = ApplyMapping.apply(frame=JoinForDepartureDetails_node1738383508715, mappings=[("carrier", "string", "carrier", "string"), ("destairportid", "long", "destairportid", "long"), ("depdelay", "long", "dep_delay", "long"), ("arrdelay", "long", "arr_delay", "long"), ("city", "string", "dep_city", "string"), ("name", "string", "dep_airport", "string"), ("state", "string", "dep_state", "string")], transformation_ctx="SchemaChangesForDepartureDetails_node1738383649894")

# Script generated for node JoinForArrivalDetails
JoinForArrivalDetails_node1738383826571 = Join.apply(frame1=SchemaChangesForDepartureDetails_node1738383649894, frame2=AirportCodesDim_node1738383311601, keys1=["destairportid"], keys2=["airport_id"], transformation_ctx="JoinForArrivalDetails_node1738383826571")

# Script generated for node SchemaChangesForArrivalDetails
SchemaChangesForArrivalDetails_node1738383884086 = ApplyMapping.apply(frame=JoinForArrivalDetails_node1738383826571, mappings=[("carrier", "string", "carrier", "string"), ("dep_delay", "long", "dep_delay", "long"), ("arr_delay", "long", "arr_delay", "long"), ("dep_city", "string", "dep_city", "string"), ("dep_airport", "string", "dep_airport", "string"), ("dep_state", "string", "dep_state", "string"), ("city", "string", "arr_city", "string"), ("name", "string", "arr_airport", "string"), ("state", "string", "arr_state", "string")], transformation_ctx="SchemaChangesForArrivalDetails_node1738383884086")

# Script generated for node WriteInTargetRedshiftTable
WriteInTargetRedshiftTable_node1738383964386 = glueContext.write_dynamic_frame.from_catalog(frame=SchemaChangesForArrivalDetails_node1738383884086, database="airlines", table_name="dev_airlines_daily_flights_processed", redshift_tmp_dir="s3://redshift-data-gds-new/write/",additional_options={"aws_iam_role": "arn:aws:iam::851725469799:role/redshift_role"}, transformation_ctx="WriteInTargetRedshiftTable_node1738383964386")

job.commit()
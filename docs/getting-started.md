# Getting started

- Sample Dataset in repo
- Detailed download + download duration
- Muss ich die Postgres-DB mit irgendwelchen Daten initialisieren? Wenn ja, wie? oder brauche ich nur eine leere Datenbank und Spark befüllt das dann alles? Schreibt am besten auf, wie das geht. 
- Muss ich Postgres benutzen oder tut's auch irgendeine andere Datenbank? Spark nutzt ja einen JDBC Treiber, das sollte wohl mit jeder beliebigen anderen DB auch tun. Ihr müsst das nicht ausprobieren, aber wenn ihr z.B. Postgres-Dumps importiert, solltet ihr darauf hinweisen, dann installiere ich lieber noch Postgres anstatt auszuprobieren, ob man das auch mit MySQL hinbekommt. 

### Requirements

1. **MusicBrainz Dataset**: A the smaller version of the dataset is sufficient
2. **Software Setup**:
   - Java: Required for running Apache Spark.
   - Python3: The primary programming language for the project.
   - Apache Spark: For handling large-scale data processing. 

   A setup guide for MacOS can be found [here](https://gist.github.com/daniel-vera-g/2c3deb6f7c0574698ac5c32a4d9913ca).

### Running

1. Start Jupyter Notebook
2. Setup Database
2. Set configuration variables at the top of the notebook
3. Run!

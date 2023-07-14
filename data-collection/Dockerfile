# Use a base Java image
FROM adoptopenjdk:11-jre-hotspot

# Set the working directory
WORKDIR /app

# Copy the JAR file to the container image
COPY target/data-collection-1.0-SNAPSHOT.jar /app

# Expose the port used by the application
EXPOSE 8080

# Define the command to run when the container starts
CMD ["java", "-jar", "data-collection-1.0-SNAPSHOT.jar"]

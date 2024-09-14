# _TraceUpscaler_

_TraceUpscaler_ is an offline tool to upscale user traffic trace (by increasing load) from open-loop latency sensitive applications.
_TraceUpscaler_ is published as a __research paper__ in Nineteenth European Conference on Computer Systems, [EuroSys 2024](https://2024.eurosys.org/).

ACM DOI Number: 10.1145/3627703.3629581.

## Abstract
Trace replay is a common approach for evaluating systems by rerunning historical traffic patterns, but it is not always possible to find suitable real-world traces at the desired level of system load. Experimenting with higher traffic loads requires upscaling a trace to artificially increase the load. Unfortunately, most prior research has adopted ad-hoc approaches for upscaling, and there has not been a systematic study of how the upscaling approach impacts the results. One common approach is to count the arrivals in a predefined time-interval and multiply these counts by a factor, but this requires generating new requests/jobs according to some model (e.g., a Poisson process), which may not be realistic. Another common approach is to divide all the timestamps in the trace by an upscaling factor to squeeze the requests into a shorter time period. However, this can distort temporal patterns within the input trace. This paper evaluates the pros and cons of existing trace upscaling techniques and introduces a new approach, _TraceUpscaler_, that avoids the drawbacks of existing methods. The key idea behind _TraceUpscaler_ is to decouple the arrival timestamps from the request parameters/data and upscale just the arrival timestamps in a way that preserves temporal patterns within the input trace.Our work applies to open-loop traffic where requests have arrival timestamps that aren't dependent on previous request completions. We evaluate _TraceUpscaler_ under multiple experimental settings using both real-world and synthetic traces. Through our study, we identify the trace characteristics that affect the quality of upscaling in existing approaches and show how _TraceUpscaler_ avoids these pitfalls. We also present a case study demonstrating how inaccurate trace upscaling can lead to incorrect conclusions about a system's ability to handle high load.



## Repository Outline
The figure here outlines the repository.

```bash
    TraceUpscaler
    ├── TraceUpscaler (gradle project)
    └── test (test helper content)
```

This repository contains a gradle project which shares the same with the repository, `TraceUpscaler`, that contains the source code for the tool.
There is another directory labeled `test`, which contains resources for quick testing of the tool.

## Requirements

The source code requires to be compiled with `Java 17`, (we used `Java Corretto 17.0.3`).
The code also uses the following libraries:

```
Apache Commons Lang 3.12.0
Apache Commons Math 3.6.1
Google Gson 2.7
```

## How to run

Please open directory  of the gradle project, `TraceUpscaler`, in your choice of IDE (we used `IntelliJ IDEA`), and run the `Test.java` file in the `org.example` package from the IDE, by changing the values of the following variables:
> __sourceTracePath__: In the main method, change the value to the absolute path of the source trace file.

> __destTracePath__:  In the main method, change the value to the destination path of the upscaled trace file.

> __scalingFactor__:  In the main method, change the value to the desired upscaling factor. 

__Note:__ Please make sure you open the gradle project in the IDE. Opening the root directory of the repository will result in the IDE not being able to detect the project inside it.
 



For ease of running _TraceUpscaler_, we have added a directory `test` which contains a jar file, `TraceUpscaler.jar` which was created from the  `TraceUpscalerRunner.java` file, with the required parameters:

> __param-1__: filepath of the trace to be upscaled (txt file)

> __param-2__: filepath of the destination of the upscaled trace (txt file)

>__param-3__: a float, which denotes the upscaling factor We also added a sample trace file, `source_trace.txt` for testing purposes. The jar file can be run with the following command format:

```
java -jar TraceUpscaler.jar param-1 param-2 param-3 
```

This should run with `Java 17+`. Please follow the following commands to run it:

```
cd test


# to store the upscaled trace in a file
#called 'upscaled_trace.txt' from the file 'source_trace.txt',
# where the upscaling factor is 2

java -jar TraceUpscaler.jar source_trace.txt upscaled_trace.txt 2

```

## Trace Format

The trace format used in this code is the following:

```
InitialStartTime;;;ActualStartTime;;;UserNumber;;;EndTime;;;Request-1;;Request-2;;..;;Request-N
```

Here is a short detail on each:

- InitialStartTime: The exact time in nanosecond when the request is supposed to arrive for servicing.
- ActualStartTime: The exact time in nanosecond when the request arrives for servicing. The difference between this and the InitialStartTime is the queueing delay.
- UserNumber: An integer which works as identifier for different users.
- EndTime: The exact time in nanosecond when the request has been served and out of the server.
- Request-X: Contains information about the request. This can change depending on the type of application we are working with. The different components of requests are separated by ';'.


# TraceScaler

_TraceScaler_ is published as a research paper in [ACM Transactions on Computer Systems](https://dl.acm.org/journal/tocs).
This is tool for scaling traces, uses [TraceSplitter](https://dl.acm.org/doi/10.1145/3447786.3456262?cid=81508684189) for downscaling and [TraceUpscaler](https://dl.acm.org/doi/10.1145/3627703.3629581?cid=81508684189) for upscaling.

ACM DOI Number: TBD

publication link: TBD

## Citing the paper

```latex
TBD
```

## Abstract

## Requirements

The code needs `Java 17+` and `Python3.7+` to run.

## Running Instruction

### Upscaling Trace

```bash
cd TraceScaler/src
python3 trace_scaler.py --sourceTraceFile <input-trace-file-path> --scalingFactor <scalingFactor>
```

**Example**

```bash
cd TraceScaler/src
python3 trace_scaler.py --sourceTraceFile files/source_trace.txt --scalingFactor 2
```

### Downsacling Trace

```bash
cd TraceScaler/src
python3 trace_scaler.py --sourceTraceFile files/source_trace.txt --scalingFactor <downscalin_factor> --downscalingScheme <downscaling_scheme>    
```

**Example**

```bash
cd TraceScaler/src
python3 trace_scaler.py --sourceTraceFile files/source_trace.txt --scalingFactor 0.5 --downscalingScheme LWL    
```

## Details of the Variables

```bash
python3 trace_scaler.py --help
usage: trace_scaler.py [-h] --sourceTraceFile Required: path of the trace to
                       be scaled
                       [--scalingFactor scaling factor for TraceScaler; For downscaling: 0 < scalingFactor <= 1; For upscaling: 1 < scalingFactor < ∞, default is 1]
                       [--downscalingScheme downscaling technique to be used, default is LWL]
                       [--bucket duration of time bucket size seconds for downscaling with AvgRateScaling , default is 1.0]

Scale the trace with TraceSplitter for downscaling or TraceUpscaler for
upscaling

optional arguments:
  -h, --help            show this help message and exit
  --sourceTraceFile Required: path of the trace to be scaled
  --scalingFactor scaling factor for TraceScaler; For downscaling: 0 < scalingFactor <= 1; For upscaling: 1 < scalingFactor < ∞, default is 1
  --downscalingScheme downscaling technique to be used, default is LWL
  --bucket duration of time bucket size (seconds) for downscaling with AvgRateScaling , default is 1.0
```

## Trace Format

The trace format used in this code is the following:

```bash
    InitialStartTime;;;ActualStartTime;;;UserNumber;;;EndTime;;;Request-1;;Request-2;;..;;Request-N
```

Here is a short detail on each part of the trace format:

- InitialStartTime: The exact time in nanosecond when the request is supposed to arrive for servicing.
- ActualStartTime: The exact time in nanosecond when the request arrives for servicing. The difference between this and the InitialStartTime is the queueing delay.
- UserNumber: An integer which works as identifier for different users.
- EndTime: The exact time in nanosecond when the request has been served and out of the server.
- Request-X: Contains information about the request. This can change depending on the type of application we are working with. The different components of requests are separated by ';'.

For more details about the implementations see [TraceUplitter Repository](https://github.com/smsajal/TraceUpscaler) and [TraceSplitter Repository](https://github.com/smsajal/TraceSplitter).

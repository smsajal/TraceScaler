import argparse
import subprocess
def scalingFactorLimit(arg):
    
    try:
        f = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be a numeric value (integer or float)")
    
    if f>=1:
        return f
    
    min = 0
    if f <= min:
        raise argparse.ArgumentTypeError(
            f"Argument must be  > {min}" )
    
    return f

def main():

    # First stage: Parse scalingFactor only
    my_parser = argparse.ArgumentParser(
        allow_abbrev=False, description='Scale the trace with TraceSplitter for downscaling or TraceUpscaler for upscaling')

    my_parser.add_argument("--sourceTraceFile", action='store', type=str, required=True,
                            metavar='path of the trace to be scaled')
    # my_parser.add_argument("--destTraceFile", action='store', type=str, required=True,
    #                         metavar='path of the trace to be scaled')
    my_parser.add_argument("--scalingFactor", action='store',
                        type=scalingFactorLimit, default=0.5, metavar='scaling factor for downscaling, 0 < scalingFactor <= 1, default is 0.5')

    # Add bucket and downscalingScheme only if scalingFactor < 1
    my_parser.add_argument("--downscalingScheme",
                        action='store', type=str, default="LWL", choices=["avgRateScaling", "tspan", "randomSampling", "RRR", "RR", "LWL"],
                        metavar='downscaling technique to be used, default is LWL')
    my_parser.add_argument("--bucket", action='store', type=float, default=1.0,
                        metavar='duration of time bucket size (seconds) for AvgRateScaling, default is 1.0')
    # Parse only traceFile and scalingFactor first
    args = my_parser.parse_args()

    # Extract the scalingFactor to determine whether to add conditional arguments
    scalingFactor = args.scalingFactor
    sourceTraceFile = args.sourceTraceFile
    
    downscalingScheme = args.downscalingScheme
    bucketSize = args.bucket
    
    if scalingFactor == 1:
        print(f"Scaling factor is {scalingFactor}, so no changes done!")
        #todo: copy the file into output file
    elif scalingFactor > 1:
        print("Doing upscaling")
        srcTraceFileSplits=sourceTraceFile.split("/")
        srcTraceFileSplits[-1]="upscaledTrace.txt"
        destTraceFile="/".join(srcTraceFileSplits)

        # java -jar TraceUpscaler.jar source_trace.txt dest_trace.txt 2
        upscaling_result=subprocess.run(['java','-jar','files/TraceUpscaler.jar',sourceTraceFile,destTraceFile,str(scalingFactor)])
        if upscaling_result.returncode!=0:
            print(f"error: {upscaling_result.stderr}")
        else:
            print("Upscaling successful!")
    else:
        print(f"Downscaling with scheme: {downscalingScheme}, bucket size: {bucketSize}")
        

    # my_parser = argparse.ArgumentParser(
    #     allow_abbrev=False, description='downscale the trace using TraceSplitter')
    # my_parser.add_argument("--traceFile", action='store',
    #                        type=str, required=True, metavar='path of the trace to be scaled')
    # my_parser.add_argument("--downscalingScheme",
    #                        action='store', type=str, default="LWL", choices=["avgRateScaling", "tspan", "randomSampling", "RRR", "RR", "LWL"], metavar='downscaling technique to be used, default is LWL')
    # my_parser.add_argument("--bucket", action='store', type=float, default=1.0,
    #                        metavar='duration of time bucket size (seconds) for downscaling with AvgRateScaling, default is 1.0')
    # my_parser.add_argument("--scalingFactor", action='store',
    #                        type=scalingFactorLimit, default=0.5, metavar='scaling factor for downscaling, 0 < scalingFactor <= 1, default is 0.5')

    # args = my_parser.parse_args()

    # traceFile = args.traceFile
    # downscalingScheme = args.downscalingScheme
    # bucketSize = args.bucket
    # scalingFactor = args.scalingFactor
    # print(f"traceFile: {traceFile}\ndownscalingScheme: {downscalingScheme}\nbucketSize: {bucketSize}\nscalingFactor: {scalingFactor}")
    
    # if scalingFactor==1:
    #     print("scaling factor is :{scalingFactor}, so no changes done!")
    # elif scalingFactor>1:
    #     print("doing upscaling")
    # else:
    #     print("doing downscaling")



    # if downscalingScheme == "avgRateScaling":
    #     avgRateScaling(traceFile, scalingFactor, bucketSize)
    # elif downscalingScheme == "tspan":
    #     timeSpanScaling(traceFile, scalingFactor)
    # elif downscalingScheme == "randomSampling":
    #     randomSampling(traceFile, scalingFactor)
    # elif downscalingScheme == "RRR":
    #     randomRoundRobinSamplingAll(traceFile, scalingFactor)
    # elif downscalingScheme == "RR":
    #     roundRobinSamplingAll(traceFile, scalingFactor)
    # elif downscalingScheme == "LWL":
    #     leastWorkLeftAll(traceFile, scalingFactor)


if __name__ == "__main__":
    main()
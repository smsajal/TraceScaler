import argparse
import subprocess
import trace_splitter.scaling_methods as ScalingMethods

infinite='\u221E'

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

    
    my_parser = argparse.ArgumentParser(
        allow_abbrev=False, description='Scale the trace with TraceSplitter for downscaling or TraceUpscaler for upscaling')

    my_parser.add_argument("--sourceTraceFile", action='store', type=str, required=True,
                            metavar='Required: path of the trace to be scaled')
                            
    my_parser.add_argument("--scalingFactor", action='store',
                        type=scalingFactorLimit, default=1, metavar=f'scaling factor for TraceScaler; For downscaling: 0 < scalingFactor <= 1; For upscaling: 1 < scalingFactor < {infinite}, default is 1')

    
    my_parser.add_argument("--downscalingScheme",
                        action='store', type=str, default="LWL", choices=["avgRateScaling", "tspan", "randomSampling", "RRR", "RR", "LWL"],
                        metavar='downscaling technique to be used, default is LWL')
    my_parser.add_argument("--bucket", action='store', type=float, default=1.0,
                        metavar='duration of time bucket size (seconds) for downscaling with AvgRateScaling , default is 1.0')
    
    args = my_parser.parse_args()

    scalingFactor = args.scalingFactor
    sourceTraceFile = args.sourceTraceFile
    downscalingScheme = args.downscalingScheme
    bucketSize = args.bucket
    
    if scalingFactor == 1:
        print(f"Scaling factor is {scalingFactor}, so no changes done!\nOutput file path: {sourceTraceFile}")
        #todo: copy the file into output file

    elif scalingFactor > 1:
        print("Doing upscaling")
        srcTraceFileSplits=sourceTraceFile.split("/")
        srcTraceFileSplits[-1]="upscaledTrace.txt"
        destTraceFile="/".join(srcTraceFileSplits)

        
        upscaling_result=subprocess.run(['java','-jar','files/TraceUpscaler.jar',sourceTraceFile,destTraceFile,str(scalingFactor)])
        if upscaling_result.returncode!=0:
            print(f"error: {upscaling_result.stderr}\n")
        else:
            print("Upscaling successful!\n")
    else:
        print(f"Downscaling with scheme: {downscalingScheme}, bucket size: {bucketSize}")
        if downscalingScheme == "LWL":
            ScalingMethods.leastWorkLeftAll(sourceTraceFile, scalingFactor)
        elif downscalingScheme == "avgRateScaling":
            ScalingMethods.avgRateScaling(sourceTraceFile, scalingFactor, bucketSize)
        elif downscalingScheme == "tspan":
            ScalingMethods.timeSpanScaling(sourceTraceFile, scalingFactor)
        elif downscalingScheme == "randomSampling":
            ScalingMethods.randomSampling(sourceTraceFile, scalingFactor)
        elif downscalingScheme == "RRR":
            ScalingMethods.randomRoundRobinSamplingAll(sourceTraceFile, scalingFactor)
        elif downscalingScheme == "RR":
            ScalingMethods.roundRobinSamplingAll(sourceTraceFile, scalingFactor)

if __name__ == "__main__":
    main()
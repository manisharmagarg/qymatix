import logging


def run_analysis(name):
    import subprocess

    try:
        # subprocess.Popen("echo Hello World", shell=True, stdout=PIPE).stdout.read()
        out = subprocess.Popen("echo Hello World", shell=True, stdout=subprocess.PIPE).stdout.read()
        cmd = "R -q -e \"CRITTERS::CRITTERS('{}')\"".format(name)
        out = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
        logging.debug(out)
        return True
    except:
        return False


def __runAnalysis(name):
    from rpy2.robjects.packages import importr

    print("Loading CRITTERS...")
    critters = importr('CRITTERS')
    print("Loading CRITTERS...loaded")
    critters.CRITTERS(name)


def _runAnalysis(name):
    from rpy2.robjects.packages import SignatureTranslatedAnonymousPackage as STAP

    # string = "library(QYMATIXFUN)\nRandomFunctions <- QYMATIXFUN::RandomFunctions"
    print("Loading CRITTERS...")
    string = "library(CRITTERS)\ncritters <- CRITTERS::CRITTERS\nq('yes')"
    rfunc = STAP(string, "rfunc")
    # rfunc.critters(user.username + "_{}".format(name))
    print("Running CRITTERS...")
    rfunc.critters(name)
    print("Running CRITTERS...finished")

    print("Loading roadmap...")
    string = "library(roadmap)\nroadmap <- roadmap::saveallresultstosql\nq('yes')"
    rfunc2 = STAP(string, "rfunc")

    # rfunc.roadmap(username=user.username + "_{}".format(name), funname="CCBM")
    # rfunc.roadmap(username=user.username + "_{}".format(name), funname="CCPM")
    # rfunc.roadmap(username=user.username + "_{}".format(name), funname="CAR")
    # rfunc.roadmap(username=user.username + "_{}".format(name), funname="PPB")

    print("Running roadmap...")
    rfunc2.roadmap(name, funname="CCBM")
    rfunc2.roadmap(name, funname="CCPM")
    print("Running roadmap...finished")


if __name__ == "__main__":
    # run("rober_data_reduced_3_xlsx")
    # runAnalysis("yoyoyo_data_1_xlsx")
    run_analysis("martin_masip")

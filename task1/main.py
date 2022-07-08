import os
import linecache

# Comments on taken approach:
#
# PROS:
# - After chunks are made, processing otput data is lightning fast, with minimal disk -> ram data transfers.
# - For processing one output, in worst case scenario, the complexity of algorithm is O(2n) where n is number of chunks.
#
# CONS:
# - Having temporary duplicate of data on disk.


# Match data from two large files in ascending order
def matchLargeFileData(fileName1, fileName2):

    CHUNK_ROWS_COUNT = 50_000 # rows count per chunk
    # only one file chunk will be loaded in memory at the time
    # rows count is arbitrary and depends on available ram memory

    # efficient representation of a file chunk
    class FileChunk:
        def __init__(self, fileName, numRows):
            self.fileName = fileName
            self.__numRows = numRows
            self.__currentRow = 1
            self.__updateInfo()

        def __del__(self):
            os.remove(self.fileName)
    
        def currentRowInfo(self):
            return self.__idx, self.__name

        def getCurrentRowIdx(self):
            return self.__currentRow;

        def getNumRows(self):
            return self.__numRows
        
        def advance(self):
            self.__currentRow += 1
            if self.__currentRow <= self.__numRows:
                self.__updateInfo()

        def __updateInfo(self):
            line = linecache.getline(self.fileName, self.__currentRow)
            self.__idx, self.__name = processLine(line)

    # get data from a line
    def processLine(line):
        line = line.split(' ')
        return int(line[1]), line[0]

    # sort chunk and save it to file
    def processChunk(chunk, chunkName):
        file = open(chunkName, 'w+')
        
        for id,name in sorted(chunk.items(), key = lambda x: x[0]):
            file.write("%s %s\n" % (name, id))
        
        file.close()

        return FileChunk(chunkName, len(chunk))

    # make chunks list from a given large file
    def chunkFile(fileName) -> list[FileChunk]:
        chunksInfo = []
        chunkData = {}

        file = open(fileName, 'r')
        for line in file:
            if len(chunkData) >= CHUNK_ROWS_COUNT:
                chunksInfo.append(processChunk(chunkData, "%s-%s.txt" % (os.path.basename(fileName), str(len(chunksInfo)))))
                chunkData = {}
            
            idx, name = processLine(line)
            chunkData[idx] = name
        file.close()

        chunksInfo.append(processChunk(chunkData, "%s-%s.txt" % (os.path.basename(fileName), str(len(chunksInfo)))))

        return chunksInfo


    # create chunks from both files
    chunks1 = chunkFile(fileName1)
    chunks2 = chunkFile(fileName2)

    # iterate given chunks yielding name and id in ascending order
    def iterateChunksInAscendingOrder(chunks: list[FileChunk]):
        lastIdx = None        
        idx = None
        name = None
        chunkObj = None

        while(len(chunks) > 0):
            idx = None
            for chunk in chunks:
                c_idx, c_name = chunk.currentRowInfo()

                if idx == None or (c_idx < idx and (lastIdx == None or idx > lastIdx)):
                    idx = c_idx
                    name = c_name
                    chunkObj = chunk
            
            lastIdx = idx

            chunkObj.advance()
            if chunkObj.getCurrentRowIdx() == chunkObj.getNumRows() + 1:
                chunks.remove(chunkObj)
            
            yield idx, name
    
    chunk1Iterator = iterateChunksInAscendingOrder(chunks1)
    chunk2Iterator = iterateChunksInAscendingOrder(chunks2)

    try:
        while True:            
            idx1, name1 = next(chunk1Iterator)
            idx2, name2 = next(chunk2Iterator)

            if idx1 != idx2:
                raise Exception('Files do not have matching data!')

            print("%s %s %d" % (name1, name2, idx1))
    except StopIteration:
        pass

matchLargeFileData('file1.txt', 'file2.txt')
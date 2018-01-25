__author__ = 'benjaminsmith'

class UnitModel(object):
    #this is a simple way to standarize how we're storing layers of units
    #right now a layer is simply a list of units.
    #it has to be a list in order to be indexable.
    #we could extend it later to be a class, possibly a class inheriting from a dictionary with minimally name and a value keys
    #but for now, the pattern is simply a name-value dictionary with optionally other values as well.
    def __init__(self,name,value):
        self.name = name
        self.value = value

    # def __new__(self,name,value):
    #     return float.__new__(self,value)

    @classmethod
    def GetLayerOfUnits(cls,layer,layer_type="UnspecifiedLayer"):
        object_type = layer_type
        try:
            #OK, let's see if we can get the necessary values.
            necessary_vals = [{"name":e["name"],"value":e["value"]} for e in layer]
            #great! if this works, for a given input, then just pass out the *original* (allow for additional values to be loaded in)
            ret_val = layer
        except TypeError as te:
            if(str(te)=="string indices must be integers, not str"):
                #seems that the iteration worked, but trying to get attributes didn't, indicating this isn't that kind of iterable.
                #let's try interpreting as a dictionary list of numeric values.
                ret_val = [{"name":k,"value":float(v)} for k,v in layer.iteritems()]
            elif (str(te)=="'int' object has no attribute '__getitem__'"):
                #probably this is a list of numeric values.
                ret_val = [{"name":object_type + str(x),"value":float(i)} for x,i in enumerate(layer)]
            elif (str(te)=="'int' object is not iterable"):
                ret_val = [{"name":object_type + str(i),"value":0.0} for i in range(0,layer)]
            else:
                ret_val=None
                raise

        return [cls(name = v["name"],value= v["value"]) for v in ret_val]

    @classmethod
    def get_list_names(cls,list):
        #this is the wrong place for this, but I wanted to avoid creating a special list class with this for as long
        #as possible; in the mean-time, this will do.
        return([li.name for li in list])

    @classmethod
    def get_list_vals(cls,list):
        #this is the wrong place for this, but I wanted to avoid creating a special list class with this for as long
        #as possible; in the mean-time, this will do.
        return([li.value for li in list])


    def __repr__(self): #let's not do this for now.
    #def __print__(self):

        return ("UnitModel " + self.name + ", value=" + str(self.value))# + super(ActionModel,self).__repr__(self))
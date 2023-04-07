'''
Fun With Python List Comprehension

Background:

For some reason, in the past I haven't always been the biggest fan of list comprehension in python, and I think partially it was for lack of a purpose for it, but also a lack of having good, real-world examples to learn from.  Most of the code examples I've seen are not very intuitive.  Stuff like:  "x for x, y and q for j in p else b or z", etc.  Who writes code like that? 

That said, in my home projects I have used the list comprehension a few times when it made sense, but recently I discovered a huge use for it, that really changed my mind and now I am a big fan of the feature.  As always, I learn by doing and hands on experimentation.

One of my side projects at home is developing a workable object model in python for QA automation testing of UI interfaces for Android and Webapps, primarily Android at the moment.  I learned Appium and Selenium, and the W3C WebDriver specification very thoroughly.  Without going into a long technical discussion of those products, I felt the need to develop my own framework to work in, which still uses some of the functionality provided by those products directly but with an entirely independent model and implementations for functionality that you would typically expect to see in an automation framework -- clicking buttons, etc.

One of the core pieces of the project is an object tree of UI elements -- python objects that are direct translations of HTML + XML DOM UI elements.  I use the python 'xml.etree.ElementTree' and 'lxml' modules to parse DOM structures from either a web page, or in Android's case, the XML "DOM" that it provides via instrumentation code that dumps all the UI elements in an XML format.  My code takes these DOM data sources, and creates Python objects with all the original attributes and tag-element hierarchy preserved.  My python objects also have methods for interacting with the elements, such as entering text data, scrolling and swiping in an app, clicking buttons, etc.

So I build a large tree of UI elements in memory representing an application.  The nodes share a common base class they inherit from, and provide specific implementations depending on type of app (web, mobile).  I can also dump the object tree to JSON using a custom serializer function.

I create the tree by adding child objects directly to parent objects as attributes.  Each node in the tree also has a Parent attribute, so you can traverse up or down or sideways through the tree, however you please.  Since every object is attached to each other using object attributes, you can use the dot-notation if you want, such as:   root.child1.child2.child3   Or in reverse:  child10.parent.parent.parent. 

Initially that was great, but to actually USE the tree and do things with it, like searching for specific combinations of parent + child nodes, I ended up having to write a lot of small, single-purpose recursive functions for traversing the tree and searching for what I want.  Like:  "Show me all the mouse-Clickable nodes which also have a Scrollable parent two levels up".

Yes, there is XPath queries but I wanted everything as native/custom python objects, not some hybrid thing.

Finally, this is how I resolved having to use a bunch of recursive functions.

I ditched all the recursions *except* for two.  Every Node in the tree has one function to traverse all the child nodes beneath it, and another function to traverse all the parent nodes above.  All relative to itself, in the same lineage.  As they traverse, they simply add each node they find to a python List object.

What this does is flatten the tree, and with the magic of iterables and iterators, I made each Node iterable, so you can do a simple "for / in" loop to walk through all the nodes of the tree without recursion.  For example, say you have a random node in the tree, you can call it as such:

   for Child in Node.Descendants():
       ...

or:

   for Parent in Node.Ancestors():
      ...
      
      
And you will get a List of every child or parent object that exists in the lineage above or below the object you are querying. You can also specify a depth or height, such as:

   for Child in Node.Descendants( 5 )
   
   
Which will limit the number of child objects in the list to 5 levels below.


That made it easier to search the tree, and since all the objects still had all their parent-child relationships intact, you can still traverse them in a list as if they were a tree but in a flat form.  In the list form of the tree, a child object may be at index 35 and its parent is at index 22, but the relationship is still intact, because each object is an attribute of another object and having them in a List doesn't change that.

I began looking into python Filters to use with "for / in" loops, and custom iterators to further enable easy-to-use queries on the lists, but then I realized, mostly by experimentation, List Comprehension is perfect for it.

First, a word about code styling.  The below examples use a very liberal amount of whitespace and that is intentional, because I would not have grasped the list comprehension as much when it is all tightly packed into a single line with cryptic single-letter variable names, like how all the online examples look like and are practically undecipherable.  If you want to see real-world examples of this type of coding style, download the Windows Research Kernel code on Github and read the Windows kernel code.  It is written by some of the smartest programmers in the world, and they use extensive amount of whitespace to keep the code as readable and understandable as possible, and it is a true enjoyment to read their code.  

All of the code examples below are valid python syntax, even though it is very spread out.

One of the key realizations I had with List Comprehension, it helps to think of it almost like writing SQL queries.  You specify the fields you want to see, the "tables" they come from, a WHERE clause to filter results by some criteria, and even JOINs on columns across multiple tables -- conceptually anyway.  The List Comprehension can be very similar.

'''

#
# To start, here is the most basic case.  
# Let us select all the Nodes in the object tree, 
# using the Root Node as the starting point.
#


    ObjectTreeRoot = CurrentPage.ElementTree
            
            
    AllNodes = ([ 
    
                    Element
                
                    for  Element  in  ObjectTreeRoot.Descendants() 
                
                ])
    
    
    print('AllNodes Count: ', len( AllNodes ))
    57
    

#
#  The above is similar to a SQL query of:   
#     
#     SELECT Element FROM ObjectTreeRoot
#
#  but not providing any WHERE clause.
#
#  So let's add one, by filtering on objects that have a clickable
#  attribute that is True.
# 
#  We can also just use the "AllNodes" list from the first example,
#  to make it even easier to read.
#


    ClickableNodes = ([ 
        
                        Element
                    
                        for  Element  in  AllNodes 
                    
                        if   Element.clickable  ==  True
                    
                     ])


    print('ClickableNodes Count: ', len( ClickableNodes ))
    8
    

#
#  The above is similar to the SQL query of:
#
#      SELECT Element FROM AllNodes WHERE clickable = True
#
#
#  Next, here we can find all of the "Leaf" nodes -- those 
#  which do not have any child objects beneath them.
#
#  And instead of including the entire Element objects,
#  We are only interested in the Name and ObjPath attributes.
#
#  It is an interesting one because Python is having to check
#  every sub-list of Descendants that every node in the tree has.
#  It's a lot of data to compare.
#



    AllLeafNodeNamesAndPaths = (

            [( 
            
                Element.Name, Element.ObjPath      ,)
          
                for  Element  in  AllNodes
                
                if   len( Element.Descendants() ) == 0
                
            ])


    print('AllLeafNodeNamesAndPaths Count: ', len( AllLeafNodeNamesAndPaths ))
    23
    
    
#
#  I'm a little rusty on my SQL but I think the above 
#   is similar to the SQL Query of:
#
#    SELECT COUNT(*), Name, ObjPath, Descendants 
#    FROM AllNodes GROUP BY Name, ObjPath WHERE Descendants = 0
#
#
#  Next, let's try joining data for two variables.
#  
#  We'll use the Ancestor relationships of the objects
#  to see how many Ancestors exist for Child objects
#  that have non-empty Text data in their 'text' attribute.
# 
#  And only wanting to see the Name of the parents,
#  and the Text data of the child objects.



   AllAncestorsOfNodesHavingTextData = (
    
            [(
            
                Parent.Name,    Child.text       ,)
          
                for  Parent       in     AllNodes
                for  Child        in     AllNodes
          
                if   Parent       in     Child.Ancestors() 
                if   Child.text   and    len( Child.text ) > 0
              
            ])

    
    print('AllAncestorsOfNodesHavingTextData Count: ', 
    len( AllAncestorsOfNodesHavingTextData ))
    161
    

#  161 results is more than the total number of objects in the tree (57).
#  it is because many of the Child objects are at the bottom of the tree heirarchy,
#  and have many ancestor objects, and many are shared among the children
#  with text data.
#
#  Next, let's try 3 levels of lineages.
#



    DescendentsOfDescendants = (
    
            [(
            
                GrandParent,  Parent,  Child     ,)
          
                for   GrandParent    in    AllNodes
                for   Parent         in    GrandParent.Descendants()
                for   Child          in    Parent.Descendants()

            ])
            
                
        print('DescendentsOfDescendants Count: ', len( DescendentsOfDescendants ))
        2486
        
        
#
#  2486 results, which is a lot, because of all the combinations of 
#  ancestors and descendents.
#
#  It did not take long to run, only a couple seconds.
#
#  Adding  a couple of "if" constraints, like this:
#


    DescendentsOfDescendants = (
    
            [(
            
                GrandParent,  Parent,  Child     ,)
          
                for   GrandParent     in    AllNodes
                for   Parent          in    GrandParent.Descendants()
                for   Child           in    Parent.Descendants()

                if    Parent          in    Child.Ancestors()
                if    GrandParent     in    Parent.Ancestors()
            ])
            

# Results in only 276 items, far less than 2486.
#
#
# Most of the actual List Comprehensions I am using for real are not as complex.
# This is an example of one that verifies whether a scrollable item is missing
# any of the 3 main components to it  (which happens when a scrollable item is 
# half-way visible on the edge of the screen).
#
#
#  Given a list of resource IDs that should not be missing:
#  Use List Comprehension to find out if we are missing anything.
#
  
 
    ChildResourceIDs = ['android:id/icon', 'android:id/title', 'android:id/summary']
    
    
    FoundChildElements  = (
    
             [( 
        
                Element, ResourceID        ,)
                
                      
                for Element in ScrollingIndexElement.Descendants()
                
                for ResourceID in ChildResourceIDs
                
                if  ResourceID in Element.resource_id 
                                
             ])
                      
                         
                         
# If the scrollable element is not missing any of the 3 IDs, the resulting List will have 3 items.
# If it is missing 1 of the IDs, the resulting list will have 2 items.
# etc.


# That's about it.  The End.






    
    In my first run I tried several layers of nodes with the activation parameter 
'selu' and got evaluating model low accuracy of .7116 and loss of .9142. Then 
I left my layers all the same but tried the 'relu' parameter instead. My 
accuracy improved slightly and loss decreased a bit. In my first two runs I 
implemented my layers with fewer nodes then categories, so on the next try I 
increased the nodes above the number of categories and got accuracy of .9663
and loss of .16. Then I went crazy and added another 5 dense layers with 15 more
nodes than categories and my accuracy came down slightly. So on the next trial I
again doubled the number of dense layers and got even worse accuracy of 0.9321.

    This didn't seem to be working well, so I removed almost all the extra dense
layers buy doubled the number of nodes per layer. This brought my accuracy close
to my best but my loss was still 0.1913. I tried taking out another dense layer
and adding even more nodes per layer. This improved my accuracy and loss by 
about a point.

    Then I tried making my layers like a funnel starting with a few layers and 
increasing for a few layers and then decreasing to the number of categories. 
This is did not help me get any better results than other trials. I tried adding
more pooling layers but got still worse.

    I got my best results eventually by doing three layers of pooling and
then I did one dense layer of 128 nodes and 50% dropout. Setting my network
like this enabled my to get loss as low as 0.1455 and accuracy as high as 
0.9629.
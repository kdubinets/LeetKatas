template <class T>
// Finish: require T to occupy no more storage than an int

static_assert(SmallType<char>);
static_assert(SmallType<int>);
static_assert(!SmallType<double> || sizeof(double) <= sizeof(int));

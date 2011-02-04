/**
*
*     TODO Doxygen documentation
*
**/


%for i in NAMESPACE:
namespace ${i}
{

%endfor

%for i in reversed(NAMESPACE):
} // namespace ${i}

%endfor



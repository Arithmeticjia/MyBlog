from haystack import indexes
# 修改此处，为你自己的model
from JiaBlog.models import Articles

# 修改此处，类名为模型类的名称+Index，比如模型类为GoodsInfo,则这里类名为GoodsInfoIndex
class ArticlesIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        # 修改此处，为你自己的model
        return Articles

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
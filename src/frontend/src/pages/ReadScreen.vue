<template>
  <div>
    本を読む画面
    <a
      href="http://localhost:8000/static/bibi/index.html?book=test.epub"
      data-bibi="embed"
      data-bibi-style="width: 100%; height: 400px;"
      >マイ・グレート・コミック</a
    >
    <!-- <script src="http://localhost:8000/static/bibi/and/jo.js"></script> -->
  </div>
</template>

<script>
export default {
  //   methods: {
  //     runScript() {
  //       // 参考:https://qiita.com/sakapun/items/7d78f48debb4fd6156cb
  //       const scripts = this.$el.querySelectorAll('script')
  //       scripts.forEach((script) => {
  //         const parentNode = script.parentNode
  //         let alternativeNode
  //         // todo: ホワイトリスト方式にする
  //         if (
  //           script.src.indexOf('http://localhost:8000/static/bibi/and/jo.js') !==
  //           -1
  //         ) {
  //           alternativeNode = document.createElement('iframe')
  //           alternativeNode.src = URL.createObjectURL(
  //             new Blob(['<!DOCTYPE html><title></title>' + script.outerHTML], {
  //               type: 'text/html',
  //             })
  //           )
  //           alternativeNode.onload = () => {
  //             alternativeNode.height =
  //               alternativeNode.contentDocument.body.scrollHeight + 50
  //           }
  //         } else {
  //           alternativeNode = document.createElement('script')
  //           alternativeNode.src = script.src
  //         }
  //         parentNode.replaceChild(alternativeNode, script)
  //       })
  //     },
  //   },
  //   mounted() {
  //     this.runScript()
  //   },
  //   updated() {
  //     this.runScript()
  //   },
}
</script>
